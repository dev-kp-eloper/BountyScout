```rust
// Update `owned.rs` to reflect the crime system and VATS matrix
#[allow(unused)]
mod owned {
    use super::*;
    
    // Update crime system status
    pub const GUARDS_AND_CRIME: bool = true;
    pub const VATS_MATRIX: Option<&'static str> = Some("1.0.0");
    
    // ... rest of the code
}

// Update the VATS section
#[allow(unused)]
mod vats {
    use super::*;
    
    pub const MATRIX_VERSION: Option<&'static str> = Some("1.0.0");
    
    // ... rest of the code
}

// Update the numeral in the inventory
#[allow(unused)]
mod inventory {
    use super::*;
    
    const fn how_many() -> usize {
        7
    }
    
    // ... rest of the code
}

// Split `inventory.rs` correctly
#[allow(unused)]
mod inventory {
    use super::*;
    
    // Split point before crime/loot feature
    if crime::is_present() {
        // ... crime feature code
    }
    
    // ... rest of the code
}
```