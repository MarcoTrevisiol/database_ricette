(function() {
    'use strict';

    angular
        .module('recipes')
        .directive('editor', EditorDirective)

        
    function EditorDirective() {
        return {
            restrict: 'E',
            bindToController: true,
            controller: 'EditorController',
            controllerAs: 'editor',
            templateUrl: 'static/editor/editor_ricetta.html',
            scope: {
                titolo: '@',
            }
        };
    };
})();
