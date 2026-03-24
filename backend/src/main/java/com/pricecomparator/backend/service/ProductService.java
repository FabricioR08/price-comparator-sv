package com.pricecomparator.backend.service;

import com.pricecomparator.backend.dto.PriceResultDTO;
import com.pricecomparator.backend.entity.Price;
import com.pricecomparator.backend.entity.Product;
import com.pricecomparator.backend.repository.PriceRepository;
import com.pricecomparator.backend.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;
    private final PriceRepository priceRepository;

    public List<PriceResultDTO> searchProductPrices(String keyword) {
        List<Product> products = productRepository.findByNameContainingIgnoreCase(keyword);
        List<PriceResultDTO> results = new ArrayList<>();

        for (Product product : products) {
            List<Price> prices = priceRepository.findByProductOrderByPriceAsc(product);
            for (Price price : prices) {
                results.add(new PriceResultDTO(
                    product.getName(),
                    price.getStore().getName(),
                    price.getPrice(),
                    price.getCurrency(),
                    price.getProductUrl(),
                    price.getLastUpdated()
                ));
            }
        }

        // Ordenar todo por precio de menor a mayor
        results.sort((a, b) -> a.getPrice().compareTo(b.getPrice()));

        return results;
    }
}