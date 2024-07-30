package com.peakperformance.peakperformance_backend.user;

public class UserRegisterRequest {

    private String email;
    private String password;

    public UserRegisterRequest(String email, String password) {
        this.email = email;
        this.password = password;
    }

    public String getEmail() {
        return email;
    }
    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }
    public void setPassword(String password) {
        this.password = password;
    }

}
