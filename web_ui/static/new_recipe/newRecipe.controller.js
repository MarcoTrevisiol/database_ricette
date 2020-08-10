(function() {
    'use strict';
    
    angular
        .module('recipes')
        .controller('NewRecipeController', NewRecipeController);

    NewRecipeController.$inject = ['RicettaFactory', 'NormalizzaDosiFactory', 'ApiRicetteFactory', '$timeout', '$log'];

    function NewRecipeController(RicettaFactory, NormalizzaDosiFactory, ApiRicetteFactory, $timeout, $log) {
        var vm = this;
        vm.MandaRichiesta = MandaRichiesta;
        vm.posto = {status: 0};
        
        
        function MandaRichiesta() {
            RicettaFactory.Carica();
            
            NormalizzaDosiFactory.Normalizza(RicettaFactory.ricetta, RicettaFactory.dosi);
            $log.log(RicettaFactory);
            ApiRicetteFactory.PostRicetta(RicettaFactory.ricetta)
                .then(function (response) {
                    NormalizzaDosiFactory.Normalizza(RicettaFactory.ricetta, 1/RicettaFactory.dosi);
                    vm.posto = {
                        status: response.status,
                        codice: response.data.codice,
                        messaggio: response.data.messaggio,
                    }
                    $log.log(response.data);
                    $timeout(function () { vm.posto.status = 0; }, 10000);
                });
        };

    };
})();
