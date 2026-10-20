/*!
 * Modo Monte · Restauración de la posición de scroll
 * ------------------------------------------------------------------
 * Al entrar a una sección (ALOJAMIENTO, UBICACIÓN, NOSOTROS, AMENITIES,
 * CAMINATAS, NUESTROS LUGARES, TIROLESA...) y salir de ella, se retoma
 * exactamente en el mismo lugar del que se salió, en lugar de volver
 * al video de portada.
 *
 * Se guarda en sessionStorage (por pestaña) la posición de:
 *   - la ventana (scroll de la página)
 *   - los paneles internos con overflow (los textos de cada sección)
 *
 * Como el sitio carga Tailwind por CDN, el alto real de la página se
 * define recien después del primer pintado. Por eso la restauración se
 * reintenta durante una ventana de tiempo y se reajusta cada vez que
 * cambia el layout, hasta que el usuario toca la rueda o la pantalla.
 */
(function () {
    'use strict';

    var STORAGE_PREFIX = 'mm:scroll:';
    var MAX_AGE = 2 * 60 * 60 * 1000;   // 2 horas
    var RETRY_WINDOW = 8000;           // ms de reintentos mientras carga el layout
    var POLL_INTERVAL = 100;           // ms entre reintentos
    var MIN_WATCH_TIME = 1500;         // ms mínimo antes de cortar la vigilancia
    var TOLERANCE = 2;                 // px de tolerancia

    /* ---------------------------------------------------------------- */
    /* Estado interno                                                    */
    /* ---------------------------------------------------------------- */
    var windowTarget = null;   // scroll objetivo de la ventana
    var panelTargets = [];     // scroll objetivo de cada panel interno
    var panels = [];           // referencias a los paneles internos
    var watching = false;      // se sigue vigilando el layout
    var userTookOver = false;  // el usuario scrolleó: no se toca más
    var deadline = 0;          // fin de la ventana de reintentos
    var satisfiedSince = 0;    // desde cuándo la posición está estable
    var startedAt = 0;
    var pollId = null;
    var lastPanelScan = 0;

    /* ---------------------------------------------------------------- */
    /* Almacenamiento                                                     */
    /* ---------------------------------------------------------------- */

    function storageKey() {
        var path = window.location.pathname.replace(/\/index\.html$/, '/');
        return STORAGE_PREFIX + path;
    }

    function readState() {
        try {
            var raw = window.sessionStorage.getItem(storageKey());
            if (!raw) return null;

            var data = JSON.parse(raw);
            if (!data || typeof data.y !== 'number' || !isFinite(data.y)) return null;

            if (Date.now() - (data.t || 0) > MAX_AGE) {
                window.sessionStorage.removeItem(storageKey());
                return null;
            }
            return data;
        } catch (err) {
            return null;
        }
    }

    function writeState(state) {
        try {
            window.sessionStorage.setItem(storageKey(), JSON.stringify(state));
        } catch (err) {
            /* modo privado o cuota llena: la navegación sigue funcionando igual */
        }
    }

    /* ---------------------------------------------------------------- */
    /* Paneles internos con scroll propio                                */
    /* ---------------------------------------------------------------- */

    function findScrollablePanels() {
        var nodes = document.body ? document.body.querySelectorAll('*') : [];
        var found = [];

        for (var i = 0; i < nodes.length; i++) {
            var overflowY = window.getComputedStyle(nodes[i]).overflowY;
            if (overflowY === 'auto' || overflowY === 'scroll') {
                found.push(nodes[i]);
            }
        }
        return found;
    }

    /* Tailwind se carga por CDN y aplica las clases recien despues del
       primer pintado: hay que volver a escanear los paneles, porque en el
       primer DOMContentLoaded todavia no tienen overflow-y-auto. El orden
       en el documento no cambia, asi que los indices siguen valiendo. */
    function refreshPanels() {
        var now = performance.now();
        if (now - lastPanelScan < 300) return;
        lastPanelScan = now;
        panels = findScrollablePanels();
    }

    function collectState() {
        var positions = [];
        for (var i = 0; i < panels.length; i++) {
            positions.push(panels[i].scrollTop);
        }

        return {
            y: window.scrollY || window.pageYOffset || 0,
            t: Date.now(),
            panels: positions
        };
    }

    /* ---------------------------------------------------------------- */
    /* Guardado                                                           */
    /* ---------------------------------------------------------------- */

    var saveQueued = false;

    function saveState() {
        refreshPanels();
        writeState(collectState());
    }

    function scheduleSave() {
        if (saveQueued) return;
        saveQueued = true;

        window.requestAnimationFrame(function () {
            saveQueued = false;
            saveState();
        });
    }

    /* ---------------------------------------------------------------- */
    /* Restauración                                                       */
    /* ---------------------------------------------------------------- */

    function maxWindowScroll() {
        var doc = document.documentElement;
        var body = document.body;
        var height = Math.max(
            doc ? doc.scrollHeight : 0,
            body ? body.scrollHeight : 0
        );
        return Math.max(0, height - window.innerHeight);
    }

    /* El scroll tiene que ser instantaneo: index.html usa scroll-smooth
       y una animacion lenta se nota mucho al volver. */
    function scrollToInstant(y) {
        var root = document.documentElement;
        var previous = root.style.scrollBehavior;
        root.style.scrollBehavior = 'auto';
        window.scrollTo(0, y);
        root.style.scrollBehavior = previous;
    }

    /* Devuelve si la posicion quedo aplicada y si todavia falta pagina
       para poder llegar al destino (la pagina aun esta Growing). */
    function applyWindowScroll() {
        if (windowTarget === null) return { applied: true, clamped: false };

        var max = maxWindowScroll();
        var y = Math.min(windowTarget, max);
        var current = window.scrollY || window.pageYOffset || 0;

        if (Math.abs(current - y) > TOLERANCE) {
            scrollToInstant(y);
        }
        return {
            applied: Math.abs(current - y) <= TOLERANCE,
            clamped: y < windowTarget
        };
    }

    function applyPanelScrolls() {
        var allApplied = true;

        for (var i = 0; i < panels.length; i++) {
            var el = panels[i];
            var target = panelTargets[i];
            if (!el || typeof target !== 'number') continue;

            var max = Math.max(0, el.scrollHeight - el.clientHeight);
            var y = Math.min(target, max);

            if (Math.abs(el.scrollTop - y) > TOLERANCE) {
                el.scrollTop = y;
                allApplied = false;
            }
        }
        return allApplied;
    }

    function poll() {
        if (!watching || userTookOver) {
            stopWatching();
            return;
        }

        refreshPanels();

        var windowState = applyWindowScroll();
        var panelsOk = applyPanelScrolls();

        // Solo se da por buena la posicion si se llego al destino de verdad.
        // Si la pagina todavia no tiene el alto suficiente, se sigue
        // esperando a que Tailwind / las imagenes terminen de cargar.
        if (windowState.applied && !windowState.clamped && panelsOk) {
            if (!satisfiedSince) satisfiedSince = performance.now();
        } else {
            satisfiedSince = 0;
        }

        var now = performance.now();
        var settled = satisfiedSince && (now - satisfiedSince) >= 400;
        var oldEnough = (now - startedAt) >= MIN_WATCH_TIME;

        if (now >= deadline || (settled && oldEnough)) {
            stopWatching();
            return;
        }

        pollId = window.setTimeout(poll, POLL_INTERVAL);
    }

    function startWatching(state) {
        windowTarget = state.y;
        panelTargets = state.panels || [];

        watching = true;
        userTookOver = false;
        satisfiedSince = 0;
        startedAt = performance.now();
        deadline = startedAt + RETRY_WINDOW;

        applyWindowScroll();
        applyPanelScrolls();

        pollId = window.setTimeout(poll, POLL_INTERVAL);
    }

    function stopWatching() {
        watching = false;
        if (pollId) {
            window.clearTimeout(pollId);
            pollId = null;
        }
        saveState();
    }

    /* Si el usuario toca la rueda o la pantalla, se deja de reajustar:
       manda el usuario, no el script. */
    function releaseTarget() {
        userTookOver = true;
        if (watching) stopWatching();
    }

    /* ---------------------------------------------------------------- */
    /* Arranque                                                           */
    /* ---------------------------------------------------------------- */

    function init() {
        // el navegador no debe restaurar el scroll por su cuenta: lo
        // hacemos nosotros para que tambien funcione con los botones
        // "volver" de cada seccion (que son navegaciones nuevas).
        try {
            window.history.scrollRestoration = 'manual';
        } catch (err) {
            /* navegadores sin soporte: se sigue con el resto */
        }

        panels = findScrollablePanels();
        lastPanelScan = performance.now();

        var state = readState();
        if (state) {
            startWatching(state);
        }

        /* --- guardado --- */
        window.addEventListener('scroll', scheduleSave, { passive: true });
        window.addEventListener('pagehide', saveState);
        window.addEventListener('beforeunload', saveState);
        document.addEventListener('visibilitychange', function () {
            if (document.visibilityState === 'hidden') saveState();
        });

        /* --- el usuario manda --- */
        window.addEventListener('wheel', releaseTarget, { passive: true });
        window.addEventListener('touchmove', releaseTarget, { passive: true });
        window.addEventListener('keydown', function (event) {
            var keys = ['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' '];
            if (keys.indexOf(event.key) !== -1) releaseTarget();
        }, true);

        /* --- bfcache: la pagina vuelve sin recargarse --- */
        window.addEventListener('pageshow', function (event) {
            if (!event.persisted) return;

            var saved = readState();
            if (!saved) return;

            windowTarget = saved.y;
            panelTargets = saved.panels || [];
            applyWindowScroll();
            applyPanelScrolls();
        });

        /* --- el alto de la pagina puede cambiar al cargar los recursos --- */
        window.addEventListener('load', function () {
            refreshPanels();

            if (!watching) {
                applyWindowScroll();
                applyPanelScrolls();
                return;
            }
            // reinicia la cuenta de estabilidad para seguir reajustando
            satisfiedSince = 0;
        });

        /* --- cambios de layout: se reajusta la posicion --- */
        if (typeof ResizeObserver === 'function' && document.body) {
            var observer = new ResizeObserver(function () {
                refreshPanels();

                if (!watching || userTookOver) return;
                applyWindowScroll();
                applyPanelScrolls();
                satisfiedSince = 0;
            });
            observer.observe(document.body);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
