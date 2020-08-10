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
    };
})();
