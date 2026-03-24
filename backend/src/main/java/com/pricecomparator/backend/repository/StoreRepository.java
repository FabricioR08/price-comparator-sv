package com.pricecomparator.backend.repository;

import com.pricecomparator.backend.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StoreRepository extends JpaRepository<Store, Long> {
}