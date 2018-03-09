var app = angular.module('evbettingodds', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');
  }]);

app.controller('odds_table', function($scope,$http) {
  $http.get('static/data.json').then(function (res){
  for (var i in res.data) {
      res.data[i]['image'] = res.data[i]['country'].toLowerCase().replace(' ','-');
  }
  $scope.data = res.data;
  });
  $http.get('static/data-top10.json').then(function (res){
    for (var i in res.data) {
      res.data[i]['image'] = res.data[i]['country'].toLowerCase().replace(' ','-');
    }
    $scope.data_top10 = res.data;
    });
  $http.get('static/data-semi1.json').then(function (res){
      for (var i in res.data) {
        res.data[i]['image'] = res.data[i]['country'].toLowerCase().replace(' ','-');
      }
      $scope.data_semi1 = res.data;
      });
  $http.get('static/data-semi2.json').then(function (res){
      for (var i in res.data) {
        res.data[i]['image'] = res.data[i]['country'].toLowerCase().replace(' ','-');
      }
      $scope.data_semi2 = res.data;
      });
  
});