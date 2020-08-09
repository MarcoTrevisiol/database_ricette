angular
    .module('recipes')
    .factory('ApiRicetteFactory', ['$http', ApiRicetteFactory])


function ApiRicetteFactory($http) {
    var url_nuova_ricetta = '/cgi-bin/main.py/nuova_ricetta';
    return {
        PostRicetta: function (ricetta) {
            return $http.post(url_nuova_ricetta, ricetta);
        },
        GetPortate: function () {
            return {
                'Primo': 'resources/Primo.jpg',
                'Secondo': 'resources/Secondo.jpg',
                'Contorno': 'resources/Contorno.jpg',
                'Dolce': 'resources/Dolce.jpg',
            };
        },
        GetPeriodi: function () {
            return {
                'Primavera': ['mar', 'apr', 'mag'],
                'Estate': ['giu', 'lug', 'ago'],
                'Autunno': ['set', 'ott', 'nov'],
                'Inverno': ['dic', 'gen', 'feb'],
                'Tutti': ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'],
                'Niente': [],
            };
        },
    };
};
