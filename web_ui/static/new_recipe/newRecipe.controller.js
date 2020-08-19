(function() {
    'use strict';
    
    angular
        .module('recipes')
        .controller('NewRecipeController', NewRecipeController);

    NewRecipeController.$inject = ['RicettaFactory', 'ApiRicetteFactory', 'ResponseFactory', '$timeout', '$location', '$log'];

    function NewRecipeController(RicettaFactory, ApiRicetteFactory, ResponseFactory, $timeout, $location, $log) {
        var vm = this;
        vm.MandaRichiesta = MandaRichiesta;
        vm.posto = ResponseFactory;
        
        
        function MandaRichiesta() {
            RicettaFactory.Carica();
            
            RicettaFactory.Normalizza(RicettaFactory.ricetta, RicettaFactory.dosi);
            $log.log(RicettaFactory);
            ApiRicetteFactory.PostRicetta(RicettaFactory.ricetta)
                .then(Ricevi);
        }
        
        function Ricevi(response) {
            RicettaFactory.Normalizza(RicettaFactory.ricetta, 1/RicettaFactory.dosi);
            vm.posto.status = response.status;
            vm.posto.codice = response.data.codice;
            vm.posto.messaggio = response.data.messaggio;
            $timeout(function () { vm.posto.status = 0; }, 10000);
            
            if (response.data.codice == 'ok') {
                $location.url('/modifica_ricetta/:' + response.data.id);
            }
        }

    }
})();
