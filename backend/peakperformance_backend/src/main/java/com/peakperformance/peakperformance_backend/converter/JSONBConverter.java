package com.peakperformance.peakperformance_backend.converter;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.peakperformance.peakperformance_backend.exercise.model.Lift;

import java.util.List;


@Converter(autoApply = true)
public class JSONBConverter implements AttributeConverter<List<Lift>, String> {

    private final ObjectMapper objectMapper;

    public JSONBConverter(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    @Override
    public String convertToDatabaseColumn(List<Lift> liftList) {
        try {
            String liftJson = objectMapper.writeValueAsString(liftList);
            return liftJson; //return JSON of lift list
        } catch (JsonProcessingException e) {
            return null;
        }
    }

    @Override
    public List<Lift> convertToEntityAttribute(String dbData) {
        try {
            return  objectMapper.readValue(dbData, new TypeReference<List<Lift>>() {});
        } catch (JsonMappingException e) {
            throw new RuntimeException();
        } catch (JsonProcessingException e) {
            throw new RuntimeException();
        }
    }

}
