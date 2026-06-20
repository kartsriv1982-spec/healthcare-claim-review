package com.aiops.authservice.service;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.aiops.authservice.dto.LoginRequest;
import com.aiops.authservice.entity.User;
import com.aiops.authservice.repository.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository repository;

    private final JwtService jwtService;

    private final PasswordEncoder encoder;

    public String login(
            LoginRequest request) {

        User user =
                repository
                        .findByUsername(
                                request.getUsername())
                        .orElseThrow(
                                () -> new RuntimeException(
                                        "User Not Found"));

        if (!request.getPassword()
                .equals(user.getPassword())) {

            throw new RuntimeException(
                    "Invalid Credentials");
        }

        return jwtService.generateToken(
                user.getUsername());
    }

    public String validate(
            String token) {

        return jwtService.validateToken(
                token);
    }
}