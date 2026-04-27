package com.example.appointments.controller;

import com.example.appointments.entity.Appointments;
import com.example.appointments.service.AppointmentsService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/appointments")
public class AppointmentsController {

    private final AppointmentsService service;

    public AppointmentsController(AppointmentsService service) {
        this.service = service;
    }

    @GetMapping("/search")
    public List<Appointments> searchAppointments(@RequestParam String doctor) {
        return service.searchByDoctor(doctor);
    }
}