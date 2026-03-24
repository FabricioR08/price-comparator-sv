package com.pricecomparator.backend.controller;

import com.pricecomparator.backend.dto.PriceResultDTO;
import com.pricecomparator.backend.service.ProductService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/products")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
@Tag(name = "Products", description = "Búsqueda y comparación de precios entre tiendas")
public class ProductController {

    private final ProductService productService;

    @GetMapping("/search")
    @Operation(
        summary = "Buscar productos por keyword",
        description = "Devuelve una lista de productos ordenados de menor a mayor precio entre todas las tiendas"
    )
    public ResponseEntity<List<PriceResultDTO>> searchProducts(
            @Parameter(description = "Nombre o parte del nombre del producto", example = "arroz")
            @RequestParam String keyword) {

        if (keyword == null || keyword.trim().isEmpty()) {
            return ResponseEntity.badRequest().build();
        }

        List<PriceResultDTO> results = productService.searchProductPrices(keyword);

        if (results.isEmpty()) {
            return ResponseEntity.noContent().build();
        }

        return ResponseEntity.ok(results);
    }
}