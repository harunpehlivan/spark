/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.spark.status.protobuf

import org.apache.spark.status.ExecutorStageSummaryWrapper
import org.apache.spark.status.api.v1.ExecutorStageSummary
import org.apache.spark.status.protobuf.Utils.getOptional

class ExecutorStageSummaryWrapperSerializer extends ProtobufSerDe {

  override val supportClass: Class[_] = classOf[ExecutorStageSummaryWrapper]

  override def serialize(input: Any): Array[Byte] =
    serialize(input.asInstanceOf[ExecutorStageSummaryWrapper])

  private def serialize(input: ExecutorStageSummaryWrapper): Array[Byte] = {
    val info = serializeExecutorStageSummary(input.info)
    val builder = StoreTypes.ExecutorStageSummaryWrapper.newBuilder()
      .setStageId(input.stageId.toLong)
      .setStageAttemptId(input.stageAttemptId)
      .setExecutorId(input.executorId)
      .setInfo(info)
    builder.build().toByteArray
  }

  def deserialize(bytes: Array[Byte]): ExecutorStageSummaryWrapper = {
    val binary = StoreTypes.ExecutorStageSummaryWrapper.parseFrom(bytes)
    val info = deserializeExecutorStageSummary(binary.getInfo)
    new ExecutorStageSummaryWrapper(
      stageId = binary.getStageId.toInt,
      stageAttemptId = binary.getStageAttemptId,
      executorId = binary.getExecutorId,
      info = info)
  }

  private def serializeExecutorStageSummary(
      input: ExecutorStageSummary): StoreTypes.ExecutorStageSummary = {
    val builder = StoreTypes.ExecutorStageSummary.newBuilder()
      .setTaskTime(input.taskTime)
      .setFailedTasks(input.failedTasks)
      .setSucceededTasks(input.succeededTasks)
      .setKilledTasks(input.killedTasks)
      .setInputBytes(input.inputBytes)
      .setInputRecords(input.inputRecords)
      .setOutputBytes(input.outputBytes)
      .setOutputRecords(input.outputRecords)
      .setShuffleRead(input.shuffleRead)
      .setShuffleReadRecords(input.shuffleReadRecords)
      .setShuffleWrite(input.shuffleWrite)
      .setShuffleWriteRecords(input.shuffleWriteRecords)
      .setMemoryBytesSpilled(input.memoryBytesSpilled)
      .setDiskBytesSpilled(input.diskBytesSpilled)
      .setIsBlacklistedForStage(input.isBlacklistedForStage)
      .setIsExcludedForStage(input.isExcludedForStage)
    input.peakMemoryMetrics.map { m =>
      builder.setPeakMemoryMetrics(ExecutorMetricsSerializer.serialize(m))
    }
    builder.build()
  }

  def deserializeExecutorStageSummary(
      binary: StoreTypes.ExecutorStageSummary): ExecutorStageSummary = {
    val peakMemoryMetrics =
      getOptional(binary.hasPeakMemoryMetrics,
        () => ExecutorMetricsSerializer.deserialize(binary.getPeakMemoryMetrics))
    new ExecutorStageSummary(
      taskTime = binary.getTaskTime,
      failedTasks = binary.getFailedTasks,
      succeededTasks = binary.getSucceededTasks,
      killedTasks = binary.getKilledTasks,
      inputBytes = binary.getInputBytes,
      inputRecords = binary.getInputRecords,
      outputBytes = binary.getOutputBytes,
      outputRecords = binary.getOutputRecords,
      shuffleRead = binary.getShuffleRead,
      shuffleReadRecords = binary.getShuffleReadRecords,
      shuffleWrite = binary.getShuffleWrite,
      shuffleWriteRecords = binary.getShuffleWriteRecords,
      memoryBytesSpilled = binary.getMemoryBytesSpilled,
      diskBytesSpilled = binary.getDiskBytesSpilled,
      isBlacklistedForStage = binary.getIsBlacklistedForStage,
      peakMemoryMetrics = peakMemoryMetrics,
      isExcludedForStage = binary.getIsExcludedForStage)
  }
}
