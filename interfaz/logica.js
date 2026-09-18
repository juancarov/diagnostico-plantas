// Ajusta esta constante si el backend corre en otro host/puerto.
const API_BASE = "http://127.0.0.1:5000/api/v1";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("diagnostico-form");
  const especieSelect = document.getElementById("especie");
  const humedadInput = document.getElementById("humedad");
  const luzInput = document.getElementById("luz");
  const temperaturaInput = document.getElementById("temperatura");
  const btn = document.getElementById("evaluar-btn");

  const resultado = document.getElementById("resultado");
  const estadoGlobalEl = document.getElementById("estado-global");
  const listaParametros = document.getElementById("lista-parametros");
  const recomendacionesWrap = document.getElementById("recomendaciones-wrap");
  const listaRecomendaciones = document.getElementById("lista-recomendaciones");
  const errorBox = document.getElementById("error-box");

  function ocultar(el) {
    el.classList.add("hidden");
  }
  function mostrar(el) {
    el.classList.remove("hidden");
  }

  function mostrarError(mensaje) {
    errorBox.textContent = mensaje;
    mostrar(errorBox);
  }

  // RF5: el selector de especie se puebla desde la API, no esta
  // escrito a mano en el HTML.
  async function cargarEspecies() {
    try {
      const respuesta = await fetch(`${API_BASE}/especies`);
      if (!respuesta.ok) {
        throw new Error("No se pudo obtener la lista de especies.");
      }
      const especies = await respuesta.json();

      // Orden alfabetico para que el selector sea usable con tantas especies.
      especies.sort((a, b) => a.nombre.localeCompare(b.nombre));

      especieSelect.innerHTML = "";
      especies.forEach((especie) => {
        const opcion = document.createElement("option");
        opcion.value = especie.nombre;
        opcion.textContent = especie.nombreComun
          ? `${especie.nombreComun} (${especie.nombre})`
          : especie.nombre;
        especieSelect.appendChild(opcion);
      });
    } catch (err) {
      especieSelect.innerHTML = '<option value="" disabled selected>No disponible</option>';
      mostrarError(
        "No se pudo cargar la lista de especies. Verifica que el backend este corriendo en " +
          API_BASE
      );
    }
  }

  function renderizarDiagnostico(data) {
    estadoGlobalEl.textContent = data.estado;
    estadoGlobalEl.className = `badge badge-${data.estado}`;

    listaParametros.innerHTML = "";
    data.parametros.forEach((p) => {
      const li = document.createElement("li");
      li.innerHTML =
        `<strong>${p.nombre}:</strong> ${p.valor} ${p.unidad} ` +
        `(óptimo ${p.rangoOptimo[0]}–${p.rangoOptimo[1]}) ` +
        `<span class="badge badge-${p.estado}">${p.estado}</span>`;
      listaParametros.appendChild(li);
    });

    listaRecomendaciones.innerHTML = "";
    if (data.recomendaciones.length === 0) {
      ocultar(recomendacionesWrap);
    } else {
      data.recomendaciones.forEach((texto) => {
        const li = document.createElement("li");
        li.textContent = texto;
        listaRecomendaciones.appendChild(li);
      });
      mostrar(recomendacionesWrap);
    }

    mostrar(resultado);
  }

  async function evaluar() {
    ocultar(errorBox);
    ocultar(resultado);

    const payload = {
      especie: especieSelect.value,
      humedad: humedadInput.value,
      luz: luzInput.value,
      temperatura: temperaturaInput.value,
    };

    btn.disabled = true;
    btn.textContent = "Evaluando...";

    try {
      const respuesta = await fetch(`${API_BASE}/diagnosticos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await respuesta.json();

      // el backend siempre manda "mensaje" en el cuerpo de error
      if (!respuesta.ok) {
        throw new Error(data.mensaje || "No se pudo evaluar la planta.");
      }

      renderizarDiagnostico(data);
    } catch (err) {
      mostrarError(err.message || "No se pudo conectar con el backend.");
    } finally {
      btn.disabled = false;
      btn.textContent = "Evaluar";
    }
  }

  btn.addEventListener("click", evaluar);
  cargarEspecies();
});
