(function() {
    'use strict';
    
    angular
        .module('recipes')
        .controller('SelectRecipeController', SelectRecipeController);

    SelectRecipeController.$inject = ['ApiRicetteFactory', 'RicettaFactory', '$log'];

    
    function SelectRecipeController(ApiRicetteFactory, RicettaFactory, $log) {
        var vm = this;
        vm.titoli = [];
        vm.ricettaHandle = RicettaFactory;
        
        activate();
        
        
        function activate() {
            ApiRicetteFactory.GetListaRicette().then(function (answer) {
                vm.titoli = answer.data;
                $log.log(answer.data);
            });
        }

    }
})();
