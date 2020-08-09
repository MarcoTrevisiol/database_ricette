(function() {
    'use strict';
    
    angular
        .module('recipes')
        .config(configRoute);
    
    configRoute.$inject = ['$routeProvider'];
    
    function configRoute($routeProvider) {
        $routeProvider
            .when('/nuova_ricetta', {
                templateUrl: 'static/new_recipe/new_recipe.html',
                controller: 'NewRecipeController',
                controllerAs: 'vm'
            })
            .otherwise('/nuova_ricetta');
    }
})();
