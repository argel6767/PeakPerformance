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
        this.objectMapper = new ObjectMapper();
    }

    @Override
    public String convertToDatabaseColumn(List<Lift> attribute) {
        String liftJSONB = "";


        return liftJSONB;
    }

    @Override
    public List<Lift> convertToEntityAttribute(String dbData) {
        List<Lift> liftList = null;
        try {
            liftList = objectMapper.readValue(dbData, new TypeReference<List<Lift>>(){});
            return liftList;
        } catch (JsonMappingException e) {
            e.printStackTrace();
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
        return liftList;
    }

}
