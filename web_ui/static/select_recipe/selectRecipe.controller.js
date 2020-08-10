(function() {
    'use strict';
    
    angular
        .module('recipes')
        .controller('SelectRecipeController', SelectRecipeController);

    SelectRecipeController.$inject = ['ApiRicetteFactory', '$log'];

    function SelectRecipeController(ApiRicetteFactory, $log) {
        var vm = this;
        vm.titoli = [];
        
        activate();
        
        
        function activate() {
            ApiRicetteFactory.GetListaRicette().then(function (answer) {
                vm.titoli = answer.data;
                $log.log(answer.data);
            });
        };

    };
})();
