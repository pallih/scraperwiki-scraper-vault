<?php

$cars = array();

$properties = array("Motorização" => "1.0", "Alimentação" => "Injeção multi ponto");

$versions = array("Ecomotion" => $properties, "Flex" => $properties);

$models = array("Golf" => $versions, "Polo" => $versions);

$brands = array("Volkswagen" => $models, "Fiat" => $models, "Ford" => $models);

$cars = $brands;

print_r($cars);