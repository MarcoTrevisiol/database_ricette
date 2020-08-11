(function() {
    'use strict';
    
    angular
        .module('recipes')
        .controller('NewRecipeController', NewRecipeController);

    NewRecipeController.$inject = ['RicettaFactory', 'ApiRicetteFactory', '$timeout', '$log'];

    function NewRecipeController(RicettaFactory, ApiRicetteFactory, $timeout, $log) {
        var vm = this;
        vm.MandaRichiesta = MandaRichiesta;
        vm.posto = {status: 0};
        
        
        function MandaRichiesta() {
            RicettaFactory.Carica();
            
            RicettaFactory.Normalizza(RicettaFactory.ricetta, RicettaFactory.dosi);
            $log.log(RicettaFactory);
            ApiRicetteFactory.PostRicetta(RicettaFactory.ricetta)
                .then(Ricevi);
        }
        
        function Ricevi(response) {
            RicettaFactory.Normalizza(RicettaFactory.ricetta, 1/RicettaFactory.dosi);
            vm.posto = {
                status: response.status,
                codice: response.data.codice,
                messaggio: response.data.messaggio,
            }
            $timeout(function () { vm.posto.status = 0; }, 10000);
        }

    }
})();
