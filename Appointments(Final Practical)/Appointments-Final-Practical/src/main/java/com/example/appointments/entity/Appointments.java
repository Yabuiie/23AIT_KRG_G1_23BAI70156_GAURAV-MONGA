package com.example.appointments.entity;

import jakarta.persistence.*;

@Entity
public class Appointments {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    private String docName;
    private String patientName;

    public Appointments(String docName, String patientName){
        this.docName = docName;
        this.patientName = patientName;
    }

    public Long getId(){
        return id;
    }

    public String getDocName(){
        return docName;
    }

    public void setDocName(String docName){
        this.docName = docName;
    }

    public String getPatientName(){
        return patientName;
    }

    public void setPatientName(String patientName) {
        this.patientName = patientName;
    }
}
