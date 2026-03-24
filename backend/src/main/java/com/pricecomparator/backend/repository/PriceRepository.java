package com.pricecomparator.backend.repository;

import com.pricecomparator.backend.entity.Price;
import com.pricecomparator.backend.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface PriceRepository extends JpaRepository<Price, Long> {
    List<Price> findByProductOrderByPriceAsc(Product product);
}