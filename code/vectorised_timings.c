#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>


#define NUM_TESTS 100
#define INPUT_SIZE 10000000


void add(int len, float* a, float* b, float* out) {
    for (int i = 0; i < len; ++i) {
        out[i] = a[i] + b[i];
    }
}

void add_vectorised(int len, float* a, float* b, float* out) {
    int i = 0;
    for (; i < len - 4; i += 4) {
        out[i] = a[i] + b[i];
        out[i + 1] = a[i + 1] + b[i + 1];
        out[i + 2] = a[i + 2] + b[i + 2];
        out[i + 3] = a[i + 3] + b[i + 3];
    }
    for (; i < len; ++i) {
        out[i] = a[i] + b[i];
    }
}

void print_timings(char* test_name, double* timings, int num_times) {
    assert(num_times > 0);

    double sum = 0.0;
    for (int i = 0; i < num_times; ++i) {
        sum += timings[i];
    }
    double avg = sum / num_times;

    double min = timings[0];
    double max = timings[0];
    for (int i = 1; i < num_times; ++i) {
        if (timings[i] < min) {
            min = timings[i];
        }
        if (timings[i] > max) {
            max = timings[i];
        }
    }

    printf(
        "%s: min=%fs, max=%fs, avg=%fs, num_tests=%d\n",
        test_name, min, max, avg, num_times);
}

int main(int argc, char* argv[]) {
    float* a = malloc(INPUT_SIZE * sizeof(float));
    float* b = malloc(INPUT_SIZE * sizeof(float));
    for (int i = 0; i < INPUT_SIZE; ++i) {
        a[i] = i;
        b[i] = i;
    }
    float* out = malloc(INPUT_SIZE * sizeof(float));

    double add_timings[NUM_TESTS] = {0};
    for (int i = 0; i < NUM_TESTS; ++i) {
        clock_t begin = clock();
        add(INPUT_SIZE, a, b, out);
        clock_t end = clock();
        add_timings[i] = (double)(end - begin) / CLOCKS_PER_SEC;
    }

    double add_vectorised_timings[NUM_TESTS] = {0};
    for (int i = 0; i < NUM_TESTS; ++i) {
        clock_t begin = clock();
        add_vectorised(INPUT_SIZE, a, b, out);
        clock_t end = clock();
        add_vectorised_timings[i] = (double)(end - begin) / CLOCKS_PER_SEC;
    }

    print_timings("Non-vectorised", add_timings, NUM_TESTS);
    print_timings("Vectorised", add_vectorised_timings, NUM_TESTS);

    free(a);
    free(b);
    free(out);
}
