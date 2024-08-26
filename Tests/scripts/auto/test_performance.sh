#!/bin/bash

# Check for required argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <number_of_iterations>"
    exit 1
fi

# Setup variables
iterations=$1
stages=("Setup" "Keygen" "Encryption" "Decryption")
schema_names=("bsw07" "myabe")
attribute_sets=("5" "10" "20" "30")
atom_sets=("5" "10" "30" "50" "100" "160" "320" "640" "1280" "1500")

# Function to execute tests
run_test() {
    local stage=$1
    local test_file=$2
    local count=$3
    echo "$count attributes/atoms >>>"
    echo ""
    for schema in "${schema_names[@]}"; do
        echo "$schema: "
        local script_name="${schema}_${test_file}.py"
        python "$script_name" $iterations $count
        echo ""
    done
}

echo "Number of iterations: $iterations"
echo "how many atom share a policy (roughly): 50"
echo ""

# Main loop to process each stage
for stage in "${stages[@]}"; do
    echo "===================================================================="
    echo "$stage"
    echo ""

    # Conditional execution based on stage type
    case $stage in
        "Setup")
            for schema in "${schema_names[@]}"; do
                echo "$schema: "
                python "${schema}_setup.py" $iterations
                echo ""
            done
            ;;
        "Keygen")
            for attrs in "${attribute_sets[@]}"; do
                run_test "$stage" "keygen" "$attrs"
            done
            ;;
        "Encryption")
            for atoms in "${atom_sets[@]}"; do
                run_test "$stage" "encryption" "$atoms"
            done
            ;;
        "Decryption")
            for atoms in "${atom_sets[@]}"; do
                run_test "$stage" "decryption" "$atoms"
            done
            ;;
    esac

    echo "===================================================================="
    echo ""
done
