def format_benchmark_report(raw_results: dict[str, list[dict]]) -> str:
    lines = ["*" * 60, "РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ", "*" * 60]

    for host, responses in raw_results.items():
        stats = collect_statistics(responses)
        lines.append(f"\nHost: {host}")
        lines.append(f"  Success: {stats['success']}")
        lines.append(f"  Failed: {stats['failed']}")
        lines.append(f"  Errors: {stats['errors']}")
        lines.append(f"  Min: {stats['min'] * 1000:.2f} ms")
        lines.append(f"  Max: {stats['max'] * 1000:.2f} ms")
        lines.append(f"  Avg: {stats['avg'] * 1000:.2f} ms")
        lines.append("-" * 40)

    return '\n'.join(lines)


def collect_statistics(responses: list[dict]) -> dict:
    success = 0
    failed = 0
    errors = 0
    times = []

    for response in responses:
        if 'error' in response:
            errors += 1

        elif 'status_code' in response:
            if 200 <= response['status_code'] < 400:
                success += 1
            else:
                failed += 1

            if 'elapsed' in response and response['elapsed'] is not None:
                times.append(response['elapsed'])

    min_time = min(times) if times else 0.0
    max_time = max(times) if times else 0.0
    avg_time = sum(times) / len(times) if times else 0.0

    return {
        'success': success,
        'failed': failed,
        'errors': errors,
        'min': min_time,
        'max': max_time,
        'avg': avg_time
    }
