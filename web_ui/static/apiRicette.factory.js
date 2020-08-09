(function() {
    'use strict';
    
    angular
        .module('recipes')
        .factory('ApiRicetteFactory', ApiRicetteFactory)

    ApiRicetteFactory.$inject = ['$http'];

    function ApiRicetteFactory($http) {
        var url_nuova_ricetta = '/cgi-bin/main.py/nuova_ricetta';
        var service = {
            PostRicetta: PostRicetta,
            GetPortate: GetPortate,
            GetPeriodi: GetPeriodi,
        };
        
        return service;
        
        
        function PostRicetta(ricetta) {
            return $http.post(url_nuova_ricetta, ricetta);
        };
        
        function GetPortate() {
            return {
                'Primo': 'resources/Primo.jpg',
                'Secondo': 'resources/Secondo.jpg',
                'Contorno': 'resources/Contorno.jpg',
                'Dolce': 'resources/Dolce.jpg',
            };
        };
        
        function GetPeriodi() {
            return {
                'Primavera': ['mar', 'apr', 'mag'],
                'Estate': ['giu', 'lug', 'ago'],
                'Autunno': ['set', 'ott', 'nov'],
                'Inverno': ['dic', 'gen', 'feb'],
                'Tutti': ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'],
                'Niente': [],
            };
        }
    };
})();
