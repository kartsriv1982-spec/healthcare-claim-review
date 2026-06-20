package com.aiops.authservice.service;

import com.aiops.authservice.dto.LoginRequest;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthServiceBack {

    private final JwtService jwtService;

    public String login(LoginRequest request) {

        log.info(
            "Authenticating user={}",
            request.getUsername()
        );

        simulateAuthFailure(request);

        return jwtService.generateToken(
                request.getUsername()
        );
    }

    public String validate(String token) {

        log.info("Validating JWT token");

        return jwtService.validateToken(token);
    }

    private void simulateAuthFailure(
            LoginRequest request
    ) {

        if ("blocked-user".equals(
                request.getUsername()
        )) {

            log.error(
                "Authentication failed for user={}",
                request.getUsername()
            );

            throw new RuntimeException(
                    "User authentication blocked"
            );
        }
    }
}