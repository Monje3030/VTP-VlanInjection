⚠️ Disclaimer

This project was developed for educational and academic purposes only as part of a Cybersecurity degree. The purpose of this repository is to demonstrate network vulnerabilities and defense mechanisms in a controlled laboratory environment.

Usage: I am not responsible for any misuse or damage caused by this software.
Ethics: Unauthorized access to networks or systems is illegal and unethical. Always perform these tests on equipment you own or have explicit permission to test.

⚠️ Descargo de Responsabilidad / Disclaimer

Este proyecto ha sido desarrollado únicamente con fines educativos y académicos como parte de mis estudios en Ciberseguridad. El propósito de este repositorio es demostrar vulnerabilidades de red y mecanismos de defensa en un entorno de laboratorio controlado.

Uso: No me hago responsable del mal uso o de los daños causados por este software.
Ética: El acceso no autorizado a redes o sistemas es ilegal y poco ético. Realiza siempre estas pruebas en equipos de tu propiedad o en aquellos donde tengas permiso explícito para realizar tests.

# 🛡️ Auditoría de Red: VTP VLAN Creation Attack

Este repositorio contiene un script de auditoría desarrollado en **Python** utilizando **Scapy**. El objetivo es demostrar las debilidades del protocolo **VTP (VLAN Trunking Protocol)** v1/v2 y cómo un atacante puede manipular la segmentación de red en una infraestructura conmutada.

## 1. Objetivo del Script
El script emula el comportamiento de un switch configurado como **VTP Server**. Mediante la inyección de tramas maliciosas, se busca forzar a los switches de la red a actualizar su base de datos `vlan.dat` con una configuración controlada por el auditor, inyectando una VLAN específica (VLAN 331).

---

## 2. Escenario de Auditoría (Topología)
Para la ejecución de esta prueba de concepto, se utilizó la siguiente topología en un entorno de laboratorio controlado:

* **Host Atacante:** Kali Linux ejecutando Scapy.
* **Switch Víctima (S1):** Cisco IOS Switch en modo VTP Server.
* **Interfaz de Conexión:** `eth0` (Kali) -> `Ethernet0/1` (Switch).

### Detalles de Direccionamiento e Interfaces
| Dispositivo | Interfaz | Rol VTP | Dominio | Password |
| :--- | :--- | :--- | :--- | :--- |
| **S1** | Et0/1 | Server | ITLA | itla |
| **Kali Linux** | eth0 | Auditor (Server) | ITLA | itla |

> **Nota:** El ataque opera en Capa 2, utilizando la dirección multicast de Cisco: `01:00:0c:cc:cc:cc`.

## 3. Parámetros Técnicos
El script utiliza los siguientes valores para garantizar la aceptación del paquete por parte del switch:

* **Domain Name:** `ITLA` (Debe ser idéntico al configurado en el switch).
* **Configuration Revision:** `65000` (Número significativamente alto para superar cualquier revisión legítima).
* **MD5 Digest:** Calculado dinámicamente incluyendo el password, el dominio y la estructura binaria de la VLAN.
* **VLAN ID / Name:** `331` / `VTP_ATTACK_331`.


## 4. Requisitos para la Herramienta
Para ejecutar este script, el entorno debe cumplir con:
1.  **Python 3.x**.
2.  **Scapy Library:** Instalable mediante `pip install scapy`.
3.  **Privilegios de Root:** Necesarios para la manipulación de sockets de Capa 2.
4.  **Enlace Troncal (Trunk):** El puerto del switch debe estar configurado como trunk o el atacante debe negociar uno mediante DTP.

---

## 5. Medidas de Mitigación
Tras la auditoría, se recomienda implementar las siguientes protecciones para neutralizar este vector de ataque:

* **VTP Mode Transparent/Off:** Es la medida más efectiva para evitar actualizaciones no deseadas.
* **Contraseñas Robustas:** Dificulta el éxito de la generación del MD5 Digest.
* **Desactivar DTP:** Configurar puertos de acceso con `switchport nonegotiate`.
* **VTP Version 3:** Ofrece mejores mecanismos de autenticación y protección de la base de datos.

---

## 6. Capturas de Referencia
1.  **S1# show vtp status** (Antes del ataque - Revisión 0).
<img width="1029" height="557" alt="image" src="https://github.com/user-attachments/assets/0906d309-6106-46f0-8811-3491d183e314" />
2.  **Kali# python3 vtp_attack.py** (Ejecución del script).
 img width="486" height="74" alt="image" src="https://github.com/user-attachments/assets/a60627b8-daea-48ff-b39c-1750f7693767" />
3.  **S1# show vlan brief** (Revision deberia cambiar, junto con la creacion de la vlan).
4.  <img width="660" height="452" alt="image" src="https://github.com/user-attachments/assets/9897b284-af61-47ee-a33e-7539440434dc" />

## 7. Enlace video de Ejemplo
https://www.youtube.com/watch?v=k2rEJPfNvAw
