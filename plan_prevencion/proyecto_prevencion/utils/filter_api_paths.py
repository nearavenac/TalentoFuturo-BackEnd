def filter_api_paths(endpoints):
    """
    Filtra los endpoints para que solo se muestren los que comienzan con /api/
    """
    filtered = []
    for path, path_regex, method, callback in endpoints:
        if path.startswith('/api/'):
            filtered.append((path, path_regex, method, callback))
    return filtered
