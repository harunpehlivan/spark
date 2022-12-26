#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# $example on$
from pyspark.mllib.evaluation import MultilabelMetrics
# $example off$
from pyspark import SparkContext

if __name__ == "__main__":
    sc = SparkContext(appName="MultiLabelMetricsExample")
    # $example on$
    scoreAndLabels = sc.parallelize([
        ([0.0, 1.0], [0.0, 2.0]),
        ([0.0, 2.0], [0.0, 1.0]),
        ([], [0.0]),
        ([2.0], [2.0]),
        ([2.0, 0.0], [2.0, 0.0]),
        ([0.0, 1.0, 2.0], [0.0, 1.0]),
        ([1.0], [1.0, 2.0])])

    # Instantiate metrics object
    metrics = MultilabelMetrics(scoreAndLabels)

    # Summary stats
    print(f"Recall = {metrics.recall()}")
    print(f"Precision = {metrics.precision()}")
    print(f"F1 measure = {metrics.f1Measure()}")
    print(f"Accuracy = {metrics.accuracy}")

    # Individual label stats
    labels = scoreAndLabels.flatMap(lambda x: x[1]).distinct().collect()
    for label in labels:
        print(f"Class {label} precision = {metrics.precision(label)}")
        print(f"Class {label} recall = {metrics.recall(label)}")
        print(f"Class {label} F1 Measure = {metrics.f1Measure(label)}")

    # Micro stats
    print(f"Micro precision = {metrics.microPrecision}")
    print(f"Micro recall = {metrics.microRecall}")
    print(f"Micro F1 measure = {metrics.microF1Measure}")

    # Hamming loss
    print(f"Hamming loss = {metrics.hammingLoss}")

    # Subset accuracy
    print(f"Subset accuracy = {metrics.subsetAccuracy}")
    # $example off$
