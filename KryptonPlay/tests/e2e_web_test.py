import os
import time

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BASE_URL = os.environ.get("KRYPTONPLAY_BASE_URL", "http://127.0.0.1:8000")
PASSWORD = os.environ["KRYPTONPLAY_ADMIN_PASSWORD"]


def wait_for_video_ready(video, timeout_ms=15000):
    video.wait_for(state="attached", timeout=timeout_ms)
    deadline = time.time() + timeout_ms / 1000
    state = None
    while time.time() < deadline:
        state = video.evaluate("v => ({readyState:v.readyState, networkState:v.networkState, error:v.error ? v.error.code : null, src:v.currentSrc || v.src, duration:v.duration})")
        if state["readyState"] >= 2:
            return state
        if state["error"] is not None:
            raise AssertionError(f"Vídeo apresentou erro de mídia: {state}")
        time.sleep(0.25)
    raise AssertionError(f"Vídeo não ficou pronto em {timeout_ms} ms: {state}")


def open_test_movie(page):
    # Click the actual playback action, not the title heading.
    card = page.locator("article.card").filter(has_text="Filme Teste").first
    card.get_by_role("button", name="Reproduzir").click()
    page.locator("#player-area").wait_for(state="visible", timeout=15000)
    page.locator("#player").wait_for(state="attached", timeout=15000)


def login(page):
    page.goto(BASE_URL, wait_until="networkidle", timeout=15000)
    page.get_by_role("button", name="Usar este servidor", exact=True).wait_for(state="visible", timeout=15000)
    page.get_by_role("button", name="Usar este servidor", exact=True).click()
    page.goto(f"{BASE_URL}/static/player.html", wait_until="networkidle", timeout=15000)
    user_card = page.locator(".user-card").filter(has_text="admin").first
    user_card.wait_for(state="visible", timeout=15000)
    user_card.click()
    password = page.locator("#password")
    password.fill(PASSWORD)
    page.get_by_role("button", name="Entrar", exact=True).click()
    page.wait_for_load_state("networkidle", timeout=15000)


def wait_for_preferences_load(page):
    with page.expect_response(
        lambda response: response.url.rstrip("/").endswith("/api/v1/profile/preferences")
        and response.request.method == "GET"
        and response.ok,
        timeout=15000,
    ):
        page.reload(wait_until="domcontentloaded", timeout=15000)


def save_preferences_and_wait(page, button):
    with page.expect_response(
        lambda response: response.url.rstrip("/").endswith("/api/v1/profile/preferences")
        and response.request.method == "PUT"
        and response.ok,
        timeout=15000,
    ) as response_info:
        button.click()
    assert response_info.value.ok, "A API de preferências recusou o salvamento."


def verify_saved_preferences(page):
    page.goto(f"{BASE_URL}/static/settings.html", wait_until="networkidle", timeout=15000)
    page.get_by_role("button", name="Aparência", exact=True).click()
    page.locator("#theme").select_option("light")
    page.locator("#language").select_option("pt-BR")
    save_preferences_and_wait(page, page.get_by_role("button", name="Salvar preferências", exact=True).first)
    # Settings pages can keep background requests/polling active; networkidle is
    # therefore not a reliable readiness condition for a reload. Wait for the
    # actual preferences GET triggered by page initialization instead.
    wait_for_preferences_load(page)
    page.get_by_role("button", name="Aparência", exact=True).click()
    assert page.locator("#theme").input_value() == "light"
    assert page.locator("#language").input_value() == "pt-BR"

    page.get_by_role("button", name="Reprodução", exact=True).click()
    page.locator("#resume").uncheck()
    page.locator("#autoplay").check()
    page.locator("#speed").select_option("1.5")
    save_preferences_and_wait(page, page.get_by_role("button", name="Salvar preferências", exact=True).last)
    wait_for_preferences_load(page)
    page.get_by_role("button", name="Reprodução", exact=True).click()
    assert page.locator("#resume").is_checked() is False
    assert page.locator("#autoplay").is_checked() is True
    assert page.locator("#speed").input_value() == "1.5"


def verify_saved_playback_behavior(page):
    page.goto(f"{BASE_URL}/static/player.html", wait_until="networkidle", timeout=15000)
    page.get_by_text("Filme Teste", exact=True).wait_for(state="visible", timeout=15000)
    open_test_movie(page)
    video = page.locator("#player")
    wait_for_video_ready(video)
    playback_rate, current_time, paused = video.evaluate("v => [v.playbackRate, v.currentTime, v.paused]")
    assert abs(playback_rate - 1.5) < 0.01, f"Velocidade padrão não foi aplicada: {playback_rate}"
    assert current_time < 1.5, f"Resume=false não foi respeitado: currentTime={current_time}"
    assert paused is False, "Autoplay=true não iniciou a reprodução."


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(15000)

        status = page.request.get(f"{BASE_URL}/api/v1/status")
        assert status.ok
        status_data = status.json()
        assert status_data["status"] == "ok"
        assert all(status_data["components"][name] == "ok" for name in ("server", "database", "library", "storage", "api"))
        assert status_data["components"]["ffmpeg"] == "ok"

        login(page)
        page.get_by_text("Filme Teste", exact=True).wait_for(state="visible", timeout=15000)
        open_test_movie(page)

        video = page.locator("#player")
        state = wait_for_video_ready(video)
        assert video.count() == 1
        assert state["src"]
        assert state["duration"] > 0

        video.evaluate("v => { v.currentTime = Math.min(1, Math.max(0, v.duration / 2)); return v.currentTime; }")
        time.sleep(0.5)
        position = video.evaluate("v => v.currentTime")
        assert position > 0

        page.wait_for_timeout(12000)
        page.get_by_role("button", name="← Voltar à biblioteca").click()
        page.locator("#player-area").wait_for(state="hidden", timeout=15000)
        page.get_by_text("Filme Teste", exact=True).wait_for(state="visible", timeout=15000)
        open_test_movie(page)

        video = page.locator("#player")
        resumed_state = wait_for_video_ready(video)
        resumed = video.evaluate("v => v.currentTime")
        assert resumed > 0, f"Progresso não foi retomado: {resumed_state}, currentTime={resumed}"

        # Verify that appearance and playback preferences persist through the real Web UI.
        verify_saved_preferences(page)
        verify_saved_playback_behavior(page)

        context.close()
        browser.close()


if __name__ == "__main__":
    try:
        main()
    except PlaywrightTimeoutError as exc:
        raise AssertionError(f"E2E atingiu timeout controlado: {exc}") from exc
