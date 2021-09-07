def create_soup(features):
    return ' '.join(features['keywords']) + ' ' + ' '.join(features['cast']) + ' ' + features['Director'] + ' ' + ' '.join(features['genres'])