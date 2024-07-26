package com.peakperformace.peakperformance_backend.converter;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.peakperformace.peakperformance_backend.exercise.model.Lift;
import com.peakperformace.peakperformance_backend.exercise.model.WeightReps;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.ArrayList;


public class JSONBConverterTest {

    private JSONBConverter converter;
    private String jsonb;
    private String jsonResponse;
    private List<Lift> lifts;

    @BeforeEach
    void init() {
        converter = new JSONBConverter(new ObjectMapper());
        lifts = new ArrayList<>();
    }

    @Test
    void testConvertToDatabaseColumnWorksWithMultipleLiftsWithDifferentExercisesAndMultipleSets() {
        jsonb = "[{\"exerciseName\":\"Deadlift\",\"sets\":[{\"weight\":150,\"reps\":8},{\"weight\":160,\"reps\":6}]},{\"exerciseName\":\"Overhead Press\",\"sets\":[{\"weight\":60,\"reps\":10},{\"weight\":65,\"reps\":8}]}]";

        lifts = List.of(
        new Lift("Deadlift", List.of(new WeightReps(150, 8), new WeightReps(160, 6))),
        new Lift("Overhead Press", List.of(new WeightReps(60, 10), new WeightReps(65, 8))));

        jsonResponse = converter.convertToDatabaseColumn(lifts);
        assertTrue(jsonResponse != null);
        assertEquals(jsonb, jsonResponse);
    }

    @Test 
    void testConvertToDatabaseColumnWorksWithOneLiftWithMultipleSets() {
        jsonb = "[{\"exerciseName\":\"Pull-Up\",\"sets\":[{\"weight\":0,\"reps\":12},{\"weight\":0,\"reps\":10},{\"weight\":0,\"reps\":8}]}]";

        lifts = List.of(
        new Lift("Pull-Up", List.of(new WeightReps(0, 12), new WeightReps(0, 10), new WeightReps(0, 8))));
        
        jsonResponse = converter.convertToDatabaseColumn(lifts);
        assertTrue(jsonResponse != null);
        assertEquals(jsonb, jsonResponse);

    }

    @Test
    void testSingleLiftingObject() {
        jsonb = "[{\"exerciseName\":\"Bench Press\",\"sets\":[{\"weight\":100,\"reps\":10}]}]";
        lifts = converter.convertToEntityAttribute(jsonb);

        assertEquals("[Lift [exerciseName=Bench Press, sets = [weight=100, reps=10], ]]", lifts.toString());
        assertEquals(1, lifts.size());
    }

    @Test
    void testConvertToEntityAttributeCorrectlyDoesNotReturnNullWithEntireListOfLifts() {
        jsonb = "[{\"exerciseName\":\"Bench Press\",\"sets\":[{\"weight\":100,\"reps\":10},{\"weight\":105,\"reps\":8},{\"weight\":110,\"reps\":6}]},{\"exerciseName\":\"Squat\",\"sets\":[{\"weight\":200,\"reps\":10},{\"weight\":210,\"reps\":8},{\"weight\":220,\"reps\":6}]}]";
        lifts = converter.convertToEntityAttribute(jsonb);

        assertTrue(lifts != null);
        assertEquals("[Lift [exerciseName=Bench Press, sets = [weight=100, reps=10],  [weight=105, reps=8],  [weight=110, reps=6], ], Lift [exerciseName=Squat, sets = [weight=200, reps=10],  [weight=210, reps=8],  [weight=220, reps=6], ]]", lifts.toString());
        assertEquals(2, lifts.size());
    }

    @Test
    void testConvertToEntityAttributeCorrectlyReturnsNullWithInvalidJson() {
        jsonb = "{\"wrongObject\":12, \"SETS\":\"23\"}";
        List<Lift> nullList = converter.convertToEntityAttribute(jsonb);
        assertNull(nullList);
    }
}
