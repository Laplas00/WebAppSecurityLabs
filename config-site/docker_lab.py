import docker

client = docker.from_env()

def get_lab_status(container_name, port=None):
    try:
        container = client.containers.get(container_name)
        status = "running"
    except docker.errors.NotFound:
        return None, "stopped", "unknown"

    vuln_marker = "/tmp/disable_vuln"
    try:
        check_cmd = f"test -f {vuln_marker}"
        exit_code, _ = container.exec_run(check_cmd)
        vuln_mode = "safe" if exit_code == 0 else "vulnerable"
    except Exception:
        vuln_mode = "unknown"

    lab_link = f"http://localhost:{port}" if port else None
    return lab_link, status, vuln_mode


def start_lab(image, container_name, port):
    try:
        try:
            existing = client.containers.get(container_name)
            existing.remove(force=True)
        except docker.errors.NotFound:
            pass

        client.containers.run(
            image,
            detach=True,
            name=container_name,
            ports={"80/tcp": port},
            remove=True
        )
        return True
    except Exception as e:
        print(f"[!] Error launching container {container_name}: {e}")
        return False


def stop_lab(container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
    except docker.errors.NotFound:
        print(f"[!] Контейнер {container_name} не найден")


def toggle_vuln(container_name):
    vuln_marker = "/tmp/disable_vuln"
    try:
        container = client.containers.get(container_name)
        check_cmd = f"test -f {vuln_marker}"
        exit_code, _ = container.exec_run(check_cmd)

        if exit_code == 0:
            container.exec_run(f"rm {vuln_marker}")
            print("[+] Уязвимость ВКЛючена.")
        else:
            container.exec_run(f"touch {vuln_marker}")
            print("[-] Уязвимость ОТКЛючена.")
    except docker.errors.NotFound:
        print("[!] Контейнер не найден.")

