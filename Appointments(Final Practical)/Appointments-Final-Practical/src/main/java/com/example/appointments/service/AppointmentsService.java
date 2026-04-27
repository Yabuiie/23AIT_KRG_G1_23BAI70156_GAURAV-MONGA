package com.example.appointments.service;

import com.example.appointments.entity.Appointments;
import com.example.appointments.repository.AppointmentsRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AppointmentsService {

    private final AppointmentsRepository repository;

    public AppointmentsService(AppointmentsRepository repository) {
        this.repository = repository;
    }

    public List<Appointments> searchByDoctor(String doctor) {
        return repository.findByDoctorNameIgnoreCase(doctor);
    }
}