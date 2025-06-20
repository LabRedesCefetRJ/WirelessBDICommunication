import json
import csv
from pathlib import Path
from statistics import stdev

# Diretório raiz onde estão os módulos
ROOT_DIR = Path("./results/")  # Ajuste conforme necessário
PROCESSED_DIR = Path("./processed_results/")  # Diretório para resultados processados

# Campos que queremos no CSV
CSV_FIELDS = [
    "module",
    "distance",
    "message_size",
    "average_elapsed",
    "best_elapsed",
    "worst_elapsed",
    "failed_attempts",
    "success_rate",
    "std_deviation"  # Nova coluna
]

# Caminho de saída do CSV consolidado
data_out = PROCESSED_DIR / "results_with_std_deviation.csv"

# Preparar escrita do CSV
with open(data_out, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
    writer.writeheader()

    # Iterar sobre cada diretório de módulo
    for module_dir in ROOT_DIR.iterdir():
        if not module_dir.is_dir():
            continue

        module_name = module_dir.name

        # Para cada subpasta de distância
        for distance_dir in module_dir.iterdir():
            if not distance_dir.is_dir():
                continue

            # Extrair valor de distância (ex: "1m" -> 1)
            dist_str = distance_dir.name.lower().rstrip('m')
            try:
                distance = float(dist_str)
            except ValueError:
                continue

            # Para cada arquivo JSON/texto na pasta de distância
            for result_file in distance_dir.glob("*.txt"):  # ou *.json
                try:
                    data = json.loads(result_file.read_text())
                except json.JSONDecodeError:
                    print(f"Falha ao ler JSON: {result_file}")
                    continue

                # Em alguns casos o objeto "results" é lista ou único
                results = data.get("results")
                if isinstance(results, list):
                    iterable = results
                else:
                    iterable = [results]

                # Normalizar resultados ao CSV
                for entry in iterable:
                    measurements = entry.get("measurements", [])
                    if isinstance(measurements, list) and len(measurements) >= 2:
                        try:
                            std_dev = round(stdev(measurements), 3)
                        except Exception as e:
                            std_dev = ""
                    else:
                        std_dev = ""  # Caso não haja medições suficientes

                    row = {
                        "module": data.get("module", module_name),
                        "distance": data.get("distance", distance),
                        "message_size": entry.get("message_size"),
                        "average_elapsed": entry.get("average_elapsed"),
                        "best_elapsed": entry.get("best_elapsed"),
                        "worst_elapsed": entry.get("worst_elapsed"),
                        "failed_attempts": entry.get("failed_attempts"),
                        "success_rate": entry.get("success_rate"),
                        "std_deviation": std_dev
                    }
                    writer.writerow(row)

print(f"CSV gerado em: {data_out.resolve()}")