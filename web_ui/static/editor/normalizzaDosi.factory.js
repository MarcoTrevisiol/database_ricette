(function() {
    'use strict';

    angular
        .module('recipes')
        .factory('NormalizzaDosiFactory', NormalizzaDosiFactory);

        
    function NormalizzaDosiFactory() {
        var service = {
            Normalizza: Normalizza,
        };
        
        return service;
        
        
        function Normalizza(ricetta, dosi) {
            for (p in ricetta.parti) {
                parte = ricetta.parti[p];
                for (i in parte.ingredienti) {
                    ingrediente = parte.ingredienti[i];
                    ingrediente.quantita.valore /= dosi;
                }
                for (v in parte.varianti) {
                    for (i in parte.varianti[v].ingredienti) {
                        ingrediente = parte.varianti[v].ingredienti[i];
                        ingrediente.quantita.valore /= dosi;
                    }
                }
            }
        }
    };
})();
