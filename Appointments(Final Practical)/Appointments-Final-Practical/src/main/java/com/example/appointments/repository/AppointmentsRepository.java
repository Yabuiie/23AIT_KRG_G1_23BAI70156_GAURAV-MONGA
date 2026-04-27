package com.example.appointments.repository;

import com.example.appointments.entity.Appointments;
import org.springframework.data.jpa.repository.*;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface AppointmentsRepository extends JpaRepository<Appointments, Long>{
    @Query("SELECT a FROM Appointment a WHERE LOWER(a.doctorName) = LOWER(:doctor)")
    List<Appointments> findByDoctorNameIgnoreCase(@Param("doctor") String doctor);
}
