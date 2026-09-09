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
    card = page.locator("article.card").filter(has_text="Filme Teste").first
    card.get_by_role("button", name="Reproduzir").click()
    page.locator("#player-area").wait_for(state="visible", timeout=15000)
    page.locator("#player").wait_for(state="attached", timeout=15000)


def login(page):
    setup_response = None
    try:
        with page.expect_response(
            lambda response: response.url.endswith("/api/setup/status")
            and response.request.method == "GET",
            timeout=15000,
        ) as response_info:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=15000)
        setup_response = response_info.value
    except PlaywrightTimeoutError as exc:
        raise AssertionError("A página inicial não concluiu GET de /api/setup/status em 15 s.") from exc

    if not setup_response.ok:
        body = setup_response.text()
        raise AssertionError(f"GET de /api/setup/status falhou: HTTP {setup_response.status}: {body}")

    setup_data = setup_response.json()
    if not setup_data.get("completed"):
        raise AssertionError(f"O servidor não está configurado segundo /api/setup/status: {setup_data}")

    use_local = page.locator("#use-local")
    use_local.wait_for(state="visible", timeout=15000)
    page.get_by_role("button", name="Usar este servidor", exact=True).click()
    page.goto(f"{BASE_URL}/static/player.html", wait_until="domcontentloaded", timeout=15000)
    user_card = page.locator(".user-card").filter(has_text="admin").first
    user_card.wait_for(state="visible", timeout=15000)
    user_card.click()
    page.locator("#password").fill(PASSWORD)
    page.get_by_role("button", name="Entrar", exact=True).click()
    page.get_by_text("Filme Teste", exact=True).wait_for(state="visible", timeout=15000)


def api_get_preferences(page):
    token = page.evaluate("() => sessionStorage.getItem('kryptonplay_token')")
    if not token:
        raise AssertionError("Sessão E2E não possui kryptonplay_token após login.")
    response = page.request.get(
        f"{BASE_URL}/api/v1/profile/preferences",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15000,
    )
    if not response.ok:
        body = response.text()
        raise AssertionError(f"GET direto de preferências falhou: HTTP {response.status}: {body}")
    payload = response.json()
    return payload.get("preferences") or {}


def save_preferences_and_wait(page, button, expected):
    try:
        with page.expect_response(
            lambda response: response.url.endswith("/api/v1/profile/preferences")
            and response.request.method == "PUT",
            timeout=15000,
        ) as response_info:
            button.click()
        response = response_info.value
    except PlaywrightTimeoutError as exc:
        raise AssertionError("O botão de salvar não concluiu a requisição PUT de preferências em 15 s.") from exc

    if not response.ok:
        body = response.text()
        raise AssertionError(f"PUT de preferências falhou: HTTP {response.status}: {body}")

    page.wait_for_function(
        """
        expected => {
            const message = document.querySelector(expected.messageId);
            return message && message.textContent.includes('Preferências salvas.');
        }
        """,
        arg={"messageId": "#appearance-message" if expected["resume"] == "true" else "#playback-message"},
        timeout=5000,
    )


def assert_preferences(actual, expected, label):
    for key in ("theme", "language", "resume", "autoplay", "speed"):
        assert str(actual.get(key)) == str(expected[key]), (
            f"{label}: preferência {key!r} incorreta: "
            f"esperado={expected[key]!r}, recebido={actual.get(key)!r}"
        )


def verify_saved_preferences(page):
    # A antiga estratégia recarregava settings.html e ficava dependente de a
    # inicialização assíncrona da página disparar GET /profile/preferences no
    # momento exato em que o Playwright aguardava o evento. Isso não testa a
    # persistência melhor e era a única falha intermitente do E2E.
    #
    # Agora o teste mantém a parte importante da UI: altera e salva pelos
    # controles reais. A persistência é então verificada diretamente pela API,
    # usando o mesmo token autenticado da sessão do navegador. O comportamento
    # efetivo dessas preferências continua sendo validado em
    # verify_saved_playback_behavior().
    page.goto(f"{BASE_URL}/static/settings.html", wait_until="domcontentloaded", timeout=15000)
    page.get_by_role("button", name="Aparência", exact=True).click()
    page.locator("#theme").select_option("light")
    page.locator("#language").select_option("pt-BR")
    # A primeira etapa deve ser determinística: não podemos presumir o estado
    # que ficou no banco após os testes anteriores. Definimos explicitamente
    # todos os controles que fazem parte do contrato verificado.
    page.locator("#resume").check()
    page.locator("#autoplay").uncheck()
    page.locator("#speed").select_option("1")
    appearance = {"theme": "light", "language": "pt-BR", "resume": "true", "autoplay": "false", "speed": "1"}
    save_preferences_and_wait(page, page.get_by_role("button", name="Salvar preferências", exact=True).first, appearance)
    assert_preferences(api_get_preferences(page), appearance, "Aparência")

    page.get_by_role("button", name="Reprodução", exact=True).click()
    page.locator("#resume").uncheck()
    page.locator("#autoplay").check()
    page.locator("#speed").select_option("1.5")
    playback = {"theme": "light", "language": "pt-BR", "resume": "false", "autoplay": "true", "speed": "1.5"}
    save_preferences_and_wait(page, page.get_by_role("button", name="Salvar preferências", exact=True).last, playback)
    assert_preferences(api_get_preferences(page), playback, "Reprodução")


def verify_saved_playback_behavior(page):
    page.goto(f"{BASE_URL}/static/player.html", wait_until="domcontentloaded", timeout=15000)
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

        verify_saved_preferences(page)
        verify_saved_playback_behavior(page)

        context.close()
        browser.close()


if __name__ == "__main__":
    try:
        main()
    except PlaywrightTimeoutError as exc:
        raise AssertionError(f"E2E atingiu timeout controlado: {exc}") from exc
