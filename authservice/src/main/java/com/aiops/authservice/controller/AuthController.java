package com.aiops.authservice.controller;

import com.aiops.authservice.dto.LoginRequest;
import com.aiops.authservice.dto.LoginResponse;
import com.aiops.authservice.service.AuthService;

import jakarta.validation.Valid;

import lombok.RequiredArgsConstructor;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    /**
     * Authenticate user and return JWT token
     */
    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(
            @Valid @RequestBody LoginRequest request) {

        String token = authService.login(request);

        return ResponseEntity.ok(
                new LoginResponse(token)
        );
    }

    /**
     * Validate JWT token
     */
    @GetMapping("/validate")
    public ResponseEntity<String> validate(
            @RequestHeader("Authorization")
            String authorizationHeader) {

        String token = authorizationHeader
                .replace("Bearer ", "");

        String username =
                authService.validate(token);

        return ResponseEntity.ok(
                "Valid Token : " + username
        );
    }

    /**
     * Health Check
     */
    @GetMapping("/health")
    public ResponseEntity<String> health() {

        return ResponseEntity.ok(
                "Auth Service UP"
        );
    }
}