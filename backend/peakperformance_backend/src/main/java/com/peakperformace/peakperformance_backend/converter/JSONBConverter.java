package com.peakperformace.peakperformance_backend.converter;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.peakperformace.peakperformance_backend.exercise.model.Lift;
import java.util.List;


@Converter
public class JSONBConverter implements AttributeConverter<List<Lift>, String> {

    private final ObjectMapper objectMapper;

    public JSONBConverter(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    @Override
    public String convertToDatabaseColumn(List<Lift> liftList) {
        String liftJson = null; //declare and inializes the liftJson
        try {
            liftJson = objectMapper.writeValueAsString(liftList);
            return liftJson; //return JSON of lift list
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
        return liftJson; //if fails will return null
    }

    @Override
    public List<Lift> convertToEntityAttribute(String dbData) {
        List<Lift> liftList = null; //declare and intialze liftlist
        try {
            liftList = objectMapper.readValue(dbData, new TypeReference<List<Lift>>(){}); //try objectmapping
            return liftList;
        } catch (JsonMappingException e) {
            e.printStackTrace();
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
        return liftList; //if some reason fails will return null
    }

}
