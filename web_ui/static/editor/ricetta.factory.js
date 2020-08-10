(function() {
    'use strict';
    
    angular
        .module('recipes')
        .factory('RicettaFactory', RicettaFactory);

    RicettaFactory.$inject = ['ModelliFactory'];
    
    function RicettaFactory(ModelliFactory) {
        var service = {
            ricetta: {
                titolo: "Titolo della ricetta",
                tempo: 'PT30M',
                parti: [ModelliFactory.Modello('partePrincipale')],
                periodo: ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'],
                categorie: [],
            },
            dosi: 4,
            Carica: function () {},
        };
        
        return service;
    };
})();
