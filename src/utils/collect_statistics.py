def collect_statistics(request_results):
    success = 0
    failed = 0
    errors = 0
    times = []
    for res in request_results:
        if 'error' in res:
            errors += 1
        elif res['is_success']:
            success += 1
            times.append(res['elapsed'])
        else:
            failed += 1
            times.append(res['elapsed'])

    if times:
        min_time = min(times)
        max_time = max(times)
        avg_time = sum(times) / len(times)
    else:
        min_time = max_time = avg_time = 0.0

    return {
        'success': success,
        'failed': failed,
        'errors': errors,
        'min': min_time,
        'max': max_time,
        'avg': avg_time
    }

