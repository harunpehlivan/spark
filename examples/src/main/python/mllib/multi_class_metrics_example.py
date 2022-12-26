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
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.util import MLUtils
from pyspark.mllib.evaluation import MulticlassMetrics
# $example off$

from pyspark import SparkContext

if __name__ == "__main__":
    sc = SparkContext(appName="MultiClassMetricsExample")

    # Several of the methods available in scala are currently missing from pyspark
    # $example on$
    # Load training data in LIBSVM format
    data = MLUtils.loadLibSVMFile(sc, "data/mllib/sample_multiclass_classification_data.txt")

    # Split data into training (60%) and test (40%)
    training, test = data.randomSplit([0.6, 0.4], seed=11)
    training.cache()

    # Run training algorithm to build the model
    model = LogisticRegressionWithLBFGS.train(training, numClasses=3)

    # Compute raw scores on the test set
    predictionAndLabels = test.map(lambda lp: (float(model.predict(lp.features)), lp.label))

    # Instantiate metrics object
    metrics = MulticlassMetrics(predictionAndLabels)

    # Overall statistics
    precision = metrics.precision(1.0)
    recall = metrics.recall(1.0)
    f1Score = metrics.fMeasure(1.0)
    print("Summary Stats")
    print(f"Precision = {precision}")
    print(f"Recall = {recall}")
    print(f"F1 Score = {f1Score}")

    # Statistics by class
    labels = data.map(lambda lp: lp.label).distinct().collect()
    for label in sorted(labels):
        print(f"Class {label} precision = {metrics.precision(label)}")
        print(f"Class {label} recall = {metrics.recall(label)}")
        print("Class %s F1 Measure = %s" % (label, metrics.fMeasure(label, beta=1.0)))

    # Weighted stats
    print(f"Weighted recall = {metrics.weightedRecall}")
    print(f"Weighted precision = {metrics.weightedPrecision}")
    print(f"Weighted F(1) Score = {metrics.weightedFMeasure()}")
    print("Weighted F(0.5) Score = %s" % metrics.weightedFMeasure(beta=0.5))
    print(f"Weighted false positive rate = {metrics.weightedFalsePositiveRate}")
    # $example off$
