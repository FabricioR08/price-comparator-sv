package com.pricecomparator.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class PriceResultDTO {
    private String productName;
    private String storeName;
    private BigDecimal price;
    private String currency;
    private String productUrl;
    private LocalDateTime lastUpdated;
}