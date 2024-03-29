(function() {
    'use strict';
    
    angular
        .module('recipes')
        .factory('ApiRicetteFactory', ApiRicetteFactory);

    ApiRicetteFactory.$inject = ['$http'];

    function ApiRicetteFactory($http) {
        var urls = {
            nuova_ricetta: '/cgi-bin/main.py/nuova_ricetta',
            lista_ricette: '/cgi-bin/main.py/lista_ricette',
            ottieni_ricetta: '/cgi-bin/main.py/ottieni_ricetta?',
            update_ricetta: '/cgi-bin/main.py/update_ricetta?',
            lista_ingredienti: '/cgi-bin/main.py/lista_ingredienti',
        };
        var service = {
            PostRicetta: PostRicetta,
            GetPortate: GetPortate,
            GetPeriodi: GetPeriodi,
            GetListaRicette: GetListaRicette,
            GetRicetta: GetRicetta,
            UpdateRicetta: UpdateRicetta,
            GetListaIngredienti: GetListaIngredienti,
        };
        
        return service;
        
        
        function PostRicetta(ricetta) {
            return $http.post(urls.nuova_ricetta, ricetta);
        }
        
        function GetPortate() {
            return {
                'Primo': 'resources/primo.jpg',
                'Secondo': 'resources/secondo.jpg',
                'Contorno': 'resources/contorno.jpg',
                'Dolce': 'resources/dolce.jpg',
            };
        }
        
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
        
        function GetListaRicette() {
            return $http.get(urls.lista_ricette);
        }
        
        function GetRicetta(ricettaId) {
            return $http.get(urls.ottieni_ricetta + ricettaId);
        }
        
        function UpdateRicetta(ricettaId, ricetta) {
            return $http.post(urls.update_ricetta + ricettaId, ricetta);
        }
        
        function GetListaIngredienti() {
            return $http.get(urls.lista_ingredienti);
        }
    }
})();
