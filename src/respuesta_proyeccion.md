## Proyección de defectos con el modelo exponencial de Musa

Se aplicó el modelo de regresión aproximado discutido en `Taller_Defectos.ipynb`. El modelo supone que la tasa instantánea de detección de defectos decae exponencialmente:

$$\lambda(t) = \lambda_0 \, e^{-(\lambda_0 / \mu_0)\, t} \qquad \mu(t) = \mu_0 \left(1 - e^{-(\lambda_0 / \mu_0)\, t}\right)$$

Ajustando una recta sobre el logaritmo de la tasa instantánea de defectos, $\ln(d) = b + m\,t$, se obtienen los parámetros:

$$\lambda_0 = e^{b} \qquad \mu_0 = -\frac{\lambda_0}{m}$$

donde $d$ son los defectos instantáneos registrados en cada intervalo (día o sesión).

### Parte 1 — Datos de los primeros días de test

| Día | Defectos |
| :--- | :--- |
| 0 | 9 |
| 1 | 18 |
| 2 | 5 |
| 3 | 7 |
| 4 | 23 |
| 5 | 2 |
| 6 | 8 |

Aplicando la regresión sobre $\ln(d)$:

$$\ln(d) = 2{,}4239 - 0{,}1151\,t$$

$$\lambda_0 = e^{2{,}4239} = 11{,}29 \qquad \mu_0 = -\frac{11{,}29}{-0{,}1151} = 98{,}12$$

Los defectos ya identificados en el período observado son $i = \sum d = 72$, por lo que la cantidad de defectos que se proyecta encontrar antes de liberar es:

$$\mu_r = \mu_0 - i = 98{,}12 - 72 = 26{,}12 \text{ defectos}$$

Proyección de defectos acumulados $\mu(t) = 98{,}12\left(1 - e^{-0{,}1151\,t}\right)$:

| Día | $\mu(t)$ | $\lambda(t)$ |
| :--- | :--- | :--- |
| 7 | 54,27 | 5,05 |
| 10 | 67,07 | 3,57 |
| 14 | 78,52 | 2,25 |
| 21 | 89,36 | 1,01 |
| 30 | 95,01 | 0,36 |

**Discusión del comportamiento.** La tasa de aparición de defectos decae en forma exponencial y tiende asintóticamente a cero a medida que $t \to \infty$, de modo que el total acumulado se estabiliza alrededor del valor proyectado $\mu_0 \approx 98$ defectos. En los primeros días el conjunto de datos es muy ruidoso (por ejemplo el pico de 23 defectos en el día 4), lo que genera una dispersión considerable respecto de la tendencia. Es importante señalar que **el modelo sólo es válido si los defectos detectados se eliminan**: si los defectos no se reparan y permanecen latentes dentro del código, la suposición de decaimiento de la tasa de detección no se cumple y la proyección pierde validez.

### Parte 2 — Dataset de resultados de prueba de la implementación Collatz

Se repite el ejercicio asimilando "Día" a "Sesión" y tomando el dataset de resultados de prueba documentado en el informe (inspección, pruebas unitarias y pruebas funcionales):

| Sesión | Fase | Defectos |
| :--- | :--- | :--- |
| 1 | Inspección de código | 6 |
| 2 | Inspección de casos de test | 2 |
| 3 | Unitaria 1 (8 ejecuciones fallidas) | 8 |
| 4 | Unitaria 2 (fallo T14) | 1 |
| 5 | Unitaria 3 (validación) | 0 |
| 6 | Funcional | 0 |

De acuerdo con la consigna, cada intento de ejecución fallido cuenta como un defecto, por lo que las 8 ejecuciones fallidas de la sesión 3 se registran como 8 defectos. Las sesiones 5 y 6 no aportan defectos y, al no poder aplicarse el logaritmo sobre cero, no intervienen en el ajuste. El conjunto efectivo es $t = \langle 1, 2, 3, 4\rangle$, $d = \langle 6, 2, 8, 1\rangle$.

Regresión sobre $\ln(d)$:

$$\ln(d) = 2{,}1383 - 0{,}3989\,t$$

$$\lambda_0 = e^{2{,}1383} = 8{,}49 \qquad \mu_0 = -\frac{8{,}49}{-0{,}3989} = 21{,}27$$

Los defectos ya identificados son $i = \sum d = 17$, entonces:

$$\mu_r = \mu_0 - i = 21{,}27 - 17 = 4{,}27 \text{ defectos liberados}$$

**Tamaño final del código.** El tamaño medido de la implementación es $S_0 = \texttt{cat collatz.py | wc -l} = 42$ LOC. Usando la densidad de defectos observada:

$$\delta = \frac{i}{S_0} = \frac{17}{42} = 0{,}4048 \text{ def/LOC}$$

el tamaño final proyectado en función de $\mu_0$ resulta:

$$S_{\text{final}} = \frac{\mu_0}{\delta} = \frac{\mu_0 \cdot S_0}{i} = \frac{21{,}27 \times 42}{17} \approx 52{,}6 \text{ LOC}$$

A modo de contraste, si se emplea la densidad de la línea de base del informe ($D = 5/18 = 0{,}2778$ def/LOC) el tamaño final sería $S = \mu_0 / D = 21{,}27 / 0{,}2778 \approx 76{,}6$ LOC.

En conclusión, el modelo proyecta alrededor de 21 defectos totales para la implementación, de los cuales 17 ya fueron detectados, por lo que quedarían del orden de 4 defectos remanentes a liberar. El código debería escalar a aproximadamente 53 LOC (o 77 LOC según la densidad de referencia) antes de alcanzar la estabilidad de detección.
