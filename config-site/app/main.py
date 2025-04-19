from flask import Flask, render_template, redirect, url_for, request
import docker
import random

# Start Flask app
app = Flask(__name__)
client = docker.from_env()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lab/sql_injection/classic')
def sql_lab_classic():
    container_name = "sql_injection_classic"
    try:
        client.containers.get(container_name)
        status = "running"
    except docker.errors.NotFound:
        status = "stopped"
        
    # If exists and running — return link
    lab_link = "http://localhost:8887" if status == "running" else None

    # Check if the lab is vulnerable
    vuln_marker = "/tmp/disable_vuln"
    try:
        container = client.containers.get(container_name)
        # Check if the vulnerability marker file exists
        check_cmd = f"test -f {vuln_marker}"
        exit_code, _ = container.exec_run(check_cmd)

        if exit_code == 0:
            vuln_mode = "safe"
        else:
            vuln_mode = "vulnerable"
    except docker.errors.NotFound:
        vuln_mode = "unknown"

    return render_template('sql_injections/sql_injection_classic.html', lab_link=lab_link, status=status, vuln_mode=vuln_mode)

@app.route('/lab/sql_injection/blind')
def sql_lab_blind():
    lab_link = "http://localhost:8886"
    status = "None"
    vuln_mode = "None"
    return render_template('sql_injections/sql_injection_blind.html', lab_link=lab_link, status=status, vuln_mode=vuln_mode)

@app.route('/lab/sql_injection/oob')
def sql_lab_oob():
    lab_link = "http://localhost:8885"
    status = "None"
    vuln_mode = "None"
    return render_template('sql_injections/sql_injection_oob.html', lab_link=lab_link, status=status, vuln_mode=vuln_mode)

@app.route('/lab/sql_injection/bypass')
def sql_lab_bypass():
    lab_link = "http://localhost:8884"
    status = "None"
    vuln_mode = "None"
    return render_template('sql_injections/sql_injection_bypass.html', lab_link=lab_link, status=status, vuln_mode=vuln_mode)


@app.route('/lab/sql_injection_classic/start', methods=['POST'])
def start_sql_lab_classic():
    lab_port = 8887
    container_name = "sql_injection_classic"

    try:
        # Check if container already exists
        existing = None
        try:
            existing = client.containers.get(container_name)
        except docker.errors.NotFound:
            pass

        # If exists but not running — remove and recreate
        if existing:
            existing.remove(force=True)

        # Run new container
        client.containers.run(
            "laplas/sql_injection_classic",
            detach=True,
            name=container_name,
            ports={"80/tcp": lab_port},
            remove=True
        )

        return redirect("/lab/sql_injection/classic")

    except Exception as e:
        return f"Launch error: {e}"

@app.route('/lab/sql_injection_classic/stop', methods=['POST'])
def stop_sql_lab():
    container = client.containers.get("sql-injection-lab")
    container.stop()
    return redirect("/lab/sql_injection")

@app.route('/lab/sql_injection_classic/toggle_vuln', methods=['POST'])
def toggle_sql_lab_vuln():
    container_name = "sql_injection_classic"
    vuln_marker = "/tmp/disable_vuln"

    try:
        container = client.containers.get(container_name)
        
        # Проверим наличие файла
        check_cmd = f"test -f {vuln_marker}"
        exit_code, _ = container.exec_run(check_cmd)

        if exit_code == 0:
            # Файл существует — удаляем (включаем уязвимость)
            container.exec_run(f"rm {vuln_marker}")
            print("[+] Уязвимость ВКЛючена.")
        else:
            # Файл не существует — создаём (отключаем уязвимость)
            container.exec_run(f"touch {vuln_marker}")
            print("[-] Уязвимость ОТКЛючена.")
    except docker.errors.NotFound:
        print("[!] Контейнер не найден.")

    return redirect("/lab/sql_injection/classic")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
