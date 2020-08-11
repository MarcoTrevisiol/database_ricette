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
            Normalizza: Normalizza,
        };
        
        return service;
    }
    
    
    function Normalizza(ricetta, dosi) {
        for (var p in ricetta.parti) {
            var parte = ricetta.parti[p];
            for (var i in parte.ingredienti) {
                var ingrediente = parte.ingredienti[i];
                ingrediente.quantita.valore /= dosi;
            }
            for (var v in parte.varianti) {
                for (var i in parte.varianti[v].ingredienti) {
                    var ingrediente = parte.varianti[v].ingredienti[i];
                    ingrediente.quantita.valore /= dosi;
                }
            }
        }
    }

})();
