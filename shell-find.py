import os

def is_supported_file(filename):
    # Daftar ekstensi file yang ingin Anda periksa (misalnya: ".php", ".txt", ".asp", dll.)
    supported_extensions = [".php", ".txt", ".asp", ".sh", ".py", ".js", ".html", ".htm", ".exe", ".dll"]
    # Tambahkan ekstensi lain yang ingin Anda periksa sesuai kebutuhan

    for ext in supported_extensions:
        if filename.endswith(ext):
            return True

    return False

def scan_file(file_path):
    # Daftar backdoor patterns untuk mendeteksi backdoor dalam berbagai jenis file
    backdoor_patterns = [
        "eval(",
        "base64_decode(",
        "system(",
        "shell_exec(",
        "passthru(",
        "exec(",
        "assert(",
        "preg_replace('/.*/e'",
        "pcntl_exec(",
        "proc_open(",
        "popen(",
        "curl_exec(",
        "include(",
        "require(",
        "eval(gzinflate(",
        # Tambahkan pola lain sesuai kebutuhan
        "backdoor_function_1(",
        "backdoor_function_2(",
        "suspicious_string_xyz",
        "suspicious_code_xyz",
        # Dan sebagainya...
    ]

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            for pattern in backdoor_patterns:
                if pattern in content:
                    return True
    except (UnicodeDecodeError, FileNotFoundError):
        pass

    return False

def scan_single_directory(directory_path):
    backdoor_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_supported_file(file_path) and scan_file(file_path):
                backdoor_files.append(file_path)

    return backdoor_files

def scan_all_directories(base_directory):
    backdoor_files = []
    for root, _, _ in os.walk(base_directory):
        backdoor_files.extend(scan_single_directory(root))

    return backdoor_files

if __name__ == "__main__":
    print("=============================================")
    print("           Analyst PHP Backdoor Finder")
    print("           zildan@jawabaratcyber.com")
    print("=============================================")
    print("Pilih salah satu opsi:")
    print("1. Scan directory tertentu")
    print("2. Scan semua directory yang berada di sini")

    choice = input("Masukkan pilihan (1/2): ")

    if choice == "1":
        directory_to_scan = input("Masukkan path directory yang ingin Anda periksa: ")
        backdoor_files = scan_single_directory(directory_to_scan)
    elif choice == "2":
        base_directory = os.getcwd()  # Menggunakan direktori kerja saat ini sebagai direktori awal
        backdoor_files = scan_all_directories(base_directory)
    else:
        print("Pilihan tidak valid.")
        exit()

    result_file = "result.txt"
    with open(result_file, "w") as f:
        if backdoor_files:
            f.write("File mencurigakan ditemukan:\n")
            for file_path in backdoor_files:
                f.write(file_path + "\n")
            print("Hasil pemindaian telah disimpan dalam file", result_file)
        else:
            f.write("Tidak ada file mencurigakan yang ditemukan dalam direktori tersebut.\n")
            print("Tidak ada file mencurigakan yang ditemukan.")

