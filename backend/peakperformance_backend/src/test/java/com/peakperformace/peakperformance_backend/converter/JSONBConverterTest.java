package com.peakperformace.peakperformance_backend.converter;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.peakperformace.peakperformance_backend.exercise.model.Lift;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;

public class JSONBConverterTest {

    private JSONBConverter converter;
    private String jsonb;

    @BeforeEach
    void init() {
        converter = new JSONBConverter(new ObjectMapper());
    }

    @Test
    void testConvertToDatabaseColumn() {

    }

    @Test
    void testSingleLiftingObject() {
        jsonb = "[{\"exerciseName\":\"Bench Press\",\"sets\":[{\"weight\":100,\"reps\":10}]}]";
        List<Lift> singleLift = converter.convertToEntityAttribute(jsonb);
        assertEquals("[Lift [exerciseName=Bench Press, sets = [weight=100, reps=10], ]]", singleLift.toString());
        assertEquals(1, singleLift.size());
    }

    @Test
    void testConvertToEntityAttributeCorrectlyDoesNotReturnNullWithEntireListOfLifts() {
        jsonb = "[{\"exerciseName\":\"Bench Press\",\"sets\":[{\"weight\":100,\"reps\":10},{\"weight\":105,\"reps\":8},{\"weight\":110,\"reps\":6}]},{\"exerciseName\":\"Squat\",\"sets\":[{\"weight\":200,\"reps\":10},{\"weight\":210,\"reps\":8},{\"weight\":220,\"reps\":6}]}]";
        List<Lift> liftList = converter.convertToEntityAttribute(jsonb);
        System.out.println(liftList.get(0).toString());
        assertTrue(liftList != null);
        assertEquals("[Lift [exerciseName=Bench Press, sets = [weight=100, reps=10],  [weight=105, reps=8],  [weight=110, reps=6], ], Lift [exerciseName=Squat, sets = [weight=200, reps=10],  [weight=210, reps=8],  [weight=220, reps=6], ]]", liftList.toString());
        assertEquals(2, liftList.size());
    }

    @Test
    void testConvertToEntityAttributeCorrectlyReturnsNullWithInvalidJson() {
        jsonb = "{\"wrongObject\":12, \"SETS\":\"23\"}";
        List<Lift> nullList = converter.convertToEntityAttribute(jsonb);
        assertNull(nullList);
    }
}
